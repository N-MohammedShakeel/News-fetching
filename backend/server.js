const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());

// GitHub Raw URL for news.json
const GITHUB_RAW_URL =
  "https://raw.githubusercontent.com/N-MohammedShakeel/News-fetching/main/news.json";

app.get("/news", async (req, res) => {
  try {
    const response = await axios.get(GITHUB_RAW_URL);
    res.json(response.data);
  } catch (error) {
    console.error("Error fetching news.json:", error);
    res.status(500).json({ message: "Failed to load news" });
  }
});

app.get("/", (req, res) => {
  res.send("Welcome to the News API. Access news at /news.");
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
