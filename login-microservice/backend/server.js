const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const db = require('./db');

const app = express();
const port = 5000;

// Middleware
app.use(express.json());  // For parsing application/json
app.use(cors());  // Enable CORS

// Secret key for JWT (use environment variables in production)
const JWT_SECRET = 'your-secret-key';

// Routes
// Serve static files from the "public" directory
const path = require('path');
app.use(express.static(path.join(__dirname, 'public')));
// Default route to serve index.html
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});
// End static files

// Registration Route
app.post('/register', (req, res) => {
  const { username, password } = req.body;

  if (!username || !password) {
    return res.status(400).json({ message: 'Username and password are required' });
  }

  // Hash the password
  bcrypt.hash(password, 10, (err, hashedPassword) => {
    if (err) {
      return res.status(500).json({ message: 'Error hashing password' });
    }

    // Insert user into the database
    db.run('INSERT INTO users (username, password) VALUES (?, ?)', [username, hashedPassword], function(err) {
      if (err) {
        return res.status(500).json({ message: 'Error creating user', error: err.message });
      }
      res.status(201).json({ message: 'User registered successfully' });
    });
  });
});

// Login Route
app.post('/login', (req, res) => {
  const { username, password } = req.body;

  if (!username || !password) {
    return res.status(400).json({ message: 'Username and password are required' });
  }

  // Fetch the user from the database
  db.get('SELECT * FROM users WHERE username = ?', [username], (err, user) => {
    if (err) {
      return res.status(500).json({ message: 'Error fetching user' });
    }

    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    // Compare the password with the stored hashed password
    bcrypt.compare(password, user.password, (err, isMatch) => {
      if (err) {
        return res.status(500).json({ message: 'Error comparing passwords' });
      }

      if (!isMatch) {
        return res.status(401).json({ message: 'Invalid credentials' });
      }

      // Create JWT token
      const token = jwt.sign({ userId: user.id }, JWT_SECRET, { expiresIn: '1h' });
      res.json({ message: 'Login successful', token });
    });
  });
});

// Protected Route (Requires JWT)
// app.get('/profile', (req, res) => {
//   const token = req.headers.authorization && req.headers.authorization.split(' ')[1];

//   if (!token) {
//     return res.status(403).json({ message: 'No token provided' });
//   }

//   // Verify the JWT token
//   jwt.verify(token, JWT_SECRET, (err, decoded) => {
//     if (err) {
//       return res.status(403).json({ message: 'Invalid or expired token' });
//     }

//     // Fetch user profile from database
//     db.get('SELECT id, username FROM users WHERE id = ?', [decoded.userId], (err, user) => {
//       if (err) {
//         return res.status(500).json({ message: 'Error fetching user profile' });
//       }

//       res.json({ message: 'User profile', user });
//     });
//   });
// });

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
