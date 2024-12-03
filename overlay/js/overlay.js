// Cache DOM elements
const elements = {
    team1Name: document.getElementById('team1-name'),
    team1Score: document.getElementById('team1-score'),
    team1Logo: document.getElementById('team1-logo'),
    team2Name: document.getElementById('team2-name'),
    team2Score: document.getElementById('team2-score'),
    team2Logo: document.getElementById('team2-logo'),
    eventStage: document.getElementById('event-stage'),
    matchTimer: document.getElementById('match-timer'),
    mapName: document.getElementById('map-name')
};

// Keep track of previous values for animation
let previousValues = {
    team1Score: '0',
    team2Score: '0'
};

// File paths configuration
const DATA_PATH = '../data/';

// Utility functions
function readFile(filename) {
    return fetch(`${DATA_PATH}${filename}.txt`)
        .then(response => response.text())
        .catch(error => console.error(`Error reading ${filename}:`, error));
}

function updateElement(element, value, animate = false) {
    if (element && value !== undefined && value !== null) {
        if (animate) {
            element.classList.add('score-changed');
            setTimeout(() => element.classList.remove('score-changed'), 300);
        }
        element.textContent = value;
    }
}

function updateColors() {
    readFile('team1_color').then(color => {
        if (color) document.documentElement.style.setProperty('--team1-color', color);
    });
    readFile('team2_color').then(color => {
        if (color) document.documentElement.style.setProperty('--team2-color', color);
    });
}

// Main update function
async function updateOverlay() {
    try {
        // Update team names
        updateElement(elements.team1Name, await readFile('team1_name'));
        updateElement(elements.team2Name, await readFile('team2_name'));

        // Update scores with animation if changed
        const team1Score = await readFile('team1_score');
        const team2Score = await readFile('team2_score');

        if (team1Score !== previousValues.team1Score) {
            updateElement(elements.team1Score, team1Score, true);
            previousValues.team1Score = team1Score;
        }

        if (team2Score !== previousValues.team2Score) {
            updateElement(elements.team2Score, team2Score, true);
            previousValues.team2Score = team2Score;
        }

        // Update other elements
        updateElement(elements.eventStage, await readFile('event_stage'));
        updateElement(elements.mapName, await readFile('map_name'));

        // Update colors
        updateColors();

    } catch (error) {
        console.error('Error updating overlay:', error);
    }
}

// Timer functions
function updateTimer() {
    const now = new Date();
    elements.matchTimer.textContent = now.toLocaleTimeString('en-US', {
        hour12: false,
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Initialize
function init() {
    // Initial update
    updateOverlay();
    updateTimer();

    // Set up intervals
    setInterval(updateOverlay, 1000); // Update overlay every second
    setInterval(updateTimer, 1000);   // Update timer every second

    // Add error handling for images
    elements.team1Logo.onerror = () => elements.team1Logo.src = '../assets/logos/default/team1.png';
    elements.team2Logo.onerror = () => elements.team2Logo.src = '../assets/logos/default/team2.png';
}

// Start when DOM is loaded
document.addEventListener('DOMContentLoaded', init);

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        updateOverlay,
        updateTimer,
        updateElement,
        readFile
    };
}
