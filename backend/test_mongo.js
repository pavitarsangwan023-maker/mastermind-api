const mongoose = require('mongoose');

const uri = "mongodb://pavitarsangwan023_db_user:AGk6aPAc9UX8z5Ag@ac-kktjpn9-shard-00-00.zwxk5l1.mongodb.net:27017,ac-kktjpn9-shard-00-01.zwxk5l1.mongodb.net:27017,ac-kktjpn9-shard-00-02.zwxk5l1.mongodb.net:27017/mastermind?ssl=true&authSource=admin&retryWrites=true&w=majority";

mongoose.connect(uri)
  .then(() => {
    console.log("SUCCESS");
    process.exit(0);
  })
  .catch(err => {
    console.error("FAIL:", err);
    process.exit(1);
  });
