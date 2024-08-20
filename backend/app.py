from fcm_utils import FcmUtils
from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras
from flask_cors import CORS

messaging = FcmUtils()
app = Flask(__name__)
CORS(app, origins=["*"])


def db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="railtel_emp_tdlist",
            user="postgres",
            password="1234",
            cursor_factory=psycopg2.extras.DictCursor,
        )
        print("Connected")
    except Exception as e:
        conn = None
        print("I'm unable to connect to database", e)
    return conn


# retrieve tokens for a user
def retrieve_tokens(email):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM "pushNotification" WHERE email=%s""", (email,))
    user_details = cursor.fetchone()
    print(user_details)

    if user_details is not None:
        print("inside retrieve", user_details)
        tokens = []
        if user_details[1] is not None:
            tokens.append(user_details[1])
        if user_details[2] is not None:
            tokens.append(user_details[2])
        return tokens


# Route to store/update tokens for a user
@app.route("/store-tokens", methods=["POST"])
def store_tokens():
    conn = db_connection()
    cursor = conn.cursor()
    data = request.get_json()
    email = "test@test.com" #FIXME: fix this
    user_agent = request.headers.get("User-Agent").lower()
    if "mobile" in user_agent:
        token_type = "mobile_token"
    else:
        token_type = "laptop_token"
    token = data["token"]

    cursor.execute("""SELECT * FROM "pushNotification" WHERE email=%s""", (email,))
    user = cursor.fetchone()

    if user is not None:  # Update the user's tokens
        print("inside update")
        cursor.execute(
            f"""UPDATE "pushNotification" SET "{token_type}"=%s WHERE email=%s""",
            (token, email),
        )
        conn.commit()
    else:
        # save new token
        print("inside store")
        cursor.execute(
            f"""INSERT INTO "pushNotification" (email, "{token_type}") VALUES(%s, %s)""",
            (email, token),
        )
        conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Token stored successfully"})


@app.route("/send-notification-to-one", methods=["GET"])
def send_notification_to_one():
    registration_tokens_single = "c6ELX-Zwo0Skdkdsml5gTv:APA91bEyTaGqSZXX5MTVWrEZeZ_tjumNVNKv9xi_9YLthQ9cGoLP4oqeHKNR7fh3H5S-LTIYYDBWSox1X9CL9uNuDlsKii5pyYcCK4FxeM4EtYd7ktZ6SfgSPvCGBcAheZxuZcYljLxg"
    title = "This is Title"
    body = "This is body"
    data = {  # if you want to send some info regarding notifications [OPTIONAL]
        "score": "850",
        "time": "2:45",
    }
    messaging.send_to_token(registration_tokens_single, title, body, data)
    return jsonify({"status": "success"})


@app.route("/send-notification-to-multiple", methods=["GET"])
def send_notification_to_multiple():
    title = "This is Title"
    body = "This is body"
    data = {  # if you want to send some info regarding notifications
        "score": "850",
        "time": "2:45",
    }
    # TODO: run this for all the users
    # emails = request.json["emails"]
    emails = ["test@test.com" #FIXME: fix this]
    for email in emails:
        tokens = retrieve_tokens(email)
        print("inside multicast", tokens)
        messaging.send_to_token_multicast(tokens, title, body, data)
    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
