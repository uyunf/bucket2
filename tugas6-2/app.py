from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.zfjim4j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    # sample_receive = request.form['sample_give']
    # print(sample_receive)
    bucket_receive = request.form['bucket_give']
    count = db.bucket.count_documents({})
    num = count + 1
    doc = {
        'num': num,
        'bucket': bucket_receive,
        'done': 0,
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': 'data saved!'})

@app.route("/bucket/delete", methods=["POST"])
def delete_post():
    # sample_receive = request.form['sample_give']
    # print(sample_receive)
    delete_receive = request.form['delete_give']
    db.bucket.delete_one({'bucket': delete_receive})
    return jsonify({'msg': 'data delete!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    # sample_receive = request.form['sample_give']
    # print(sample_receive)
    num_receive = request.form['num_give']
    db.bucket.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'update done!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': bucket_list})




if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)