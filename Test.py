<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Simple Quiz</title>
    <link rel="stylesheet" href="quiz.css">
</head>
<body>
    <!-- User Info Form -->
    <div id="user-info">
        <img src="C:/Users/Ayoub/Desktop/JS/Quiz App/SG.png" alt="Quiz Logo" id="quiz-logo" />
        <input type="text" id="user-fullname" placeholder="Enter your full name" required />
        <div id="fullname-alert" class="input-alert"></div> 
        <input type="email" id="user-email" placeholder="Enter your email address" required />
        <div id="email-alert" class="input-alert"></div>
        <button type="button" id="start-quiz-btn">Start Quiz</button>
    </div>

    <!-- Quiz App -->
    <div class="app" style="display: none;">
        <h1>Simple Quiz</h1>
        <div id="quiz" class="quiz">
            <h2 id="question"></h2>
            <div id="answer-buttons" class="answer-buttons"></div>
            <div id="multiple-choice-text" class="multiple-choice-text" style="display: none;"></div>
            <button id="submit-btn" class="btn" style="display: none;">Submit</button>
            <button id="next-btn" class="btn" style="display: none;">Next</button>
            <!-- Bouton 'Retake the Quiz', initialement masqué -->
            <button id="retake-quiz-btn" class="btn" style="display: none;">Retake the Quiz</button>
        </div>
    </div>

    <script src="quiz.js"></script>
</body>
</html>
let currentQuestionIndex, score, currentRetries = 0;
const maxRetries = 3; // Limite de tentatives
const questions = [
    // ... (Vos questions ici)
];

// ... (Autres déclarations initiales)

function startQuiz() {
    currentRetries = 0; // Réinitialiser les tentatives à chaque nouveau départ
    // ... (Autre logique de démarrage du quiz)
}

// ... (Autres fonctions)

function endQuiz() {
    // ... (Logique existante pour la fin du quiz)
    if (currentRetries < maxRetries) {
        document.getElementById('retake-quiz-btn').style.display = 'inline'; // Afficher le bouton pour recommencer
    } else {
        // Logique facultative si l'utilisateur atteint la limite de tentatives
    }
}

function retakeQuiz() {
    currentRetries++;
    currentQuestionIndex = 0;
    score = 0;
    document.getElementById('quiz').style.display = 'block';
    document.getElementById('result-container').remove(); // Assurez-vous que cette div existe
    showQuestion();
}

document.getElementById('retake-quiz-btn').addEventListener('click', retakeQuiz);

// ... (Reste de vos fonctions et gestionnaires d'événements)

// Exemple de fonction showQuestion
function showQuestion() {
    // ... (Votre logique pour afficher une question)
}

// ... (Autres fonctions et gestionnaires d'événements nécessaires)

let currentQuestionIndex, score, currentRetries = 0;
const maxRetries = 3; // Limite de tentatives

// ... (Autres déclarations et fonctions)

function startQuiz() {
    currentRetries = 0; // Réinitialisez les tentatives
    // ... (Le reste de la logique de startQuiz)
}

function endQuiz() {
    // ... (Logique existante d'affichage des résultats)
    if (currentRetries < maxRetries) {
        const retakeButton = document