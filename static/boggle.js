class BoggleGame {
    constructor() {
        this.form = $("#form");
        this.result = $("#result");
        this.scoreDisplay = $("#score");
        this.score = 0;
        this.timeDisplay = $("#time");
        this.time = 60;
        this.playedWords = new Set();
        this.form.on("submit", this.handleSubmit.bind(this));
        this.startTimer();
    }

    startTimer() {
        this.timer = setInterval(() => {
            this.time--;
            this.timeDisplay.text(`Time: ${this.time}`);
            if (this.time <= 0) {
                clearInterval(this.timer);
                this.endGame();
            }
        }, 1000)
    }

    async endGame() {
        this.form.find("button").attr("disabled", true);
        this.result.text("Time's Up! ");
        await this.sendScore();
    }

    async sendScore() {
        const response = await fetch('/end-game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ score: this.score })
        });
        const data = await response.json();
    }

    async handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(this.form[0]);
        const response = await fetch('/check-word', {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        this.result.text(data.result);
        if (data.result === "ok") {
            const word = $("#word").val();
            if (this.playedWords.has(word)) {
                this.result.text("Word already used");
                return;
            }
            this.playedWords.add(word);
            this.updateScore(word.length);
        }
    }

    updateScore(wordLen) {
        this.score += wordLen;
        this.scoreDisplay.text(`Score: ${this.score}`);
    }
}

$(document).ready(function() {
    new BoggleGame();
});
