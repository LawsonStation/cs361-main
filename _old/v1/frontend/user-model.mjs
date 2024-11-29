// user-model.mjs
import mongoose from 'mongoose';

const { Schema } = mongoose;

// Define the schema
const userSchema = new Schema({
  _id: {
    type: mongoose.Types.ObjectId,
    default: () => new mongoose.Types.ObjectId(),
  },
  username: {
    type: String,
    required: true,
    unique: true,
  },
  email: {
    type: String,
    required: true,
    unique: true,
    match: /.+\@.+\..+/,
  },
  password: {
    type: String,
    required: true,
  },
}, { timestamps: true });

// Export the model
const User = mongoose.model('User', userSchema);
export default User;
