const express = require('express');
const dotenv = require('dotenv');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const app = express();
dotenv.config();

const API_URL = process.env.API_URL;
const EFS_LOG_PATH = process.env.EFS_LOG_PATH; // Menggunakan nilai dari .env

// Middleware untuk menyimpan log ke file
app.use((req, res, next) => {
    const logMessage = `${new Date().toISOString()} - ${req.method} ${req.url} - ${req.ip}\n`;
    fs.appendFile(EFS_LOG_PATH, logMessage, (err) => {
        if (err) {
            console.error('Error writing to log file:', err);
        }
    });
    next();
});

app.use(express.static('public'));
app.use(express.json());

app.set('view engine', 'ejs');

app.get('/', (req, res) => {
    const ip_address = req.ip;
    res.render('index', { ip_address });
});

app.get('/get_books', async (req, res) => {
    try {
        const response = await axios.get(API_URL);
        const books = JSON.parse(response.data.body);
        const logMessage = `${new Date().toISOString()} - GET /get_books - ${req.ip}\n`;
        fs.appendFile(EFS_LOG_PATH, logMessage, (err) => {
            if (err) {
                console.error('Error writing to log file:', err);
            }
        });
        res.json(books);
    } catch (error) {
        console.error('Error fetching books:', error); // Log kesalahan
        res.status(500).json({ error: 'Internal Server Error' });
    }
});


app.post('/add_book', (req, res) => {
    const { title } = req.body;
    // Logic to add book
    res.json({ message: 'Book added successfully' });
});

app.listen(5000, () => {
    console.log('Server is running on port 5000');
});
