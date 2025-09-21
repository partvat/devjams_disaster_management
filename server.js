// server.js
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Example endpoint to register user
app.post('/register', (req, res) => {
    const { name, phone, latitude, longitude } = req.body;

    console.log('User Info:', name, phone, latitude, longitude);

    // Here you can save the info to a database
    // Or send SMS using TextBee/Twilio

    res.send({ success: true, message: 'User registered successfully!' });
});

// Start server
const PORT = 3000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
