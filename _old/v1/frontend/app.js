// app.js
const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const User = require('./models/User');

const app = express();

// Middleware to parse form data
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files from the 'public' directory
app.use(express.static('public'));

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/yourDatabase', {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => console.log('Connected to MongoDB'))
  .catch(error => console.log(error));

// Handle form submission
app.post('/register', async (req, res) => {
    const { username, email, password } = req.body;
    try {
        // Create a new user document
        const user = new User({ username, email, password });
        await user.save();
        res.send("User registered successfully!");
    } catch (error) {
        res.status(400).send("Error registering user: " + error.message);
    }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
