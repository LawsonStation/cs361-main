// Models for the items Collection

// Import dependencies.
import mongoose from 'mongoose';
import 'dotenv/config';

// Connect based on the .env file parameters.
mongoose.connect(
    process.env.MONGODB_CONNECT_STRING,
    { useNewUrlParser: true }
);
const db = mongoose.connection;

// Confirm that the database has connected and print a message in the console.
db.once("open", (err) => {
    if(err){
        res.status(500).json({ Error: 'Error establishing database connection.' });
    } else  {
        console.log('Success: Database connection successful.');
    }
});

// Define the schema
const itemSchema = mongoose.Schema({
    title: {
      type: String,
      required: true
    },
    currency: {
      type: String,
      default: 'USD'
    },
    description: {
      type: String,
      required: true
    },
    images: {
      type: [Buffer], // Buffer for binary image data
      required: true,
    },
    location: {
      city: {
        type: String,
        required: true
      },
      state: {
        type: String,
        required: true
      },
      country: {
        type: String,
        required: true
      },
      zip: {
        type: String,
        required: true
      }
    },
    posted_at: {
      type: Date,
      default: Date.now
    },
    posted_by: {
      type: mongoose.Types.ObjectId,
      required: true,
      ref: 'User' 
    },
    price: {
      type: Number,
      required: true
    },
    status: {
      type: String,
      enum: ['available', 'sold', 'reserved'],
      default: 'available'
    }
  });
  
  // Export the model
  const Item = mongoose.model('Item', itemSchema);
  export default Item;
  