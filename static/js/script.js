
document.addEventListener('DOMContentLoaded', function() {
    // Elementos do formulário de previsão
    const predictForm = document.getElementById('predict-form');
   
    // Elementos de exibição da previsão
    const predictionValue = document.getElementById('prediction-value');
    const timerDisplay = document.getElementById('timer');
    const progressBar = document.getElementById('progress-bar');
    const historyContainer = document.getElementById('history-container');
   
    // Se estamos na página do dashboard
    if (predictForm) {
        // Carrega o histórico inicial
        fetchHistory();
       
        // Adiciona o evento de submit ao formulário
        predictForm.addEventListener('submit', function(e) {
            e.preventDefault();
            generatePrediction();
        });
    }
   
    // Função para gerar uma previsão
    function generatePrediction() {
        const formData = new FormData(predictForm);
       
        fetch('/api/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
           
            // Atualiza a UI com a previsão
            updatePredictionDisplay(data.prediction, data.wait_time);
           
            // Adiciona a previsão ao histórico
            addToHistory(data.prediction);
        })
        .catch(error => {
            console.error('Erro ao gerar previsão:', error);
            alert('Erro ao gerar previsão. Tente novamente.');
        });
    }
   
    // Função para buscar o histórico
    function fetchHistory() {
        fetch('/api/history')
        .then(response => response.json())
        .then(data => {
            if (data.history) {
                updateHistoryDisplay(data.history);
            }
        })
        .catch(error => {
            console.error('Erro ao buscar histórico:', error);
        });
    }
   
    // Função para atualizar a exibição da previsão
    function updatePredictionDisplay(prediction, waitTime) {
        // Define a cor baseada no valor da previsão
        let colorClass = '';
       
        const predValue = parseFloat(prediction);
        if (predValue >= 1.00 && predValue <= 1.59) {
            colorClass = 'blue-number';
        } else if (predValue >= 2.00 && predValue <= 9.59) {
            colorClass = 'purple-number';
        } else {
            colorClass = 'pink-number';
        }
       
        // Remove classes de cor anteriores
        predictionValue.classList.remove('blue-number', 'purple-number', 'pink-number');
       
        // Adiciona a nova classe de cor
        predictionValue.classList.add(colorClass);
       
        // Exibe a previsão
        predictionValue.textContent = prediction;
       
        // Inicia o timer
        startTimer(waitTime);
    }
   
    // Função para iniciar o timer
    function startTimer(seconds) {
        let timeLeft = seconds;
        timerDisplay.textContent = timeLeft;
       
        // Reseta a barra de progresso
        progressBar.style.width = '0%';
       
        // Animação da barra de progresso
        progressBar.style.width = '100%';
        progressBar.style.transition = `width ${seconds}s linear`;
       
        // Atualiza o timer a cada segundo
        const timerInterval = setInterval(() => {
            timeLeft--;
           
            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                timerDisplay.textContent = '0';
               
                // Após o término do timer, exibe "--" na previsão
                setTimeout(() => {
                    predictionValue.textContent = '--.--';
                    predictionValue.classList.remove('blue-number', 'purple-number', 'pink-number');
                    progressBar.style.width = '0%';
                    progressBar.style.transition = 'none';
                }, 1000);
            } else {
                timerDisplay.textContent = timeLeft;
            }
        }, 1000);
    }
   
    // Função para adicionar uma previsão ao histórico
    function addToHistory(prediction) {
        // Se o histórico já estiver cheio (5 itens), remove o mais antigo
        if (historyContainer.children.length >= 5) {
            historyContainer.removeChild(historyContainer.lastChild);
        }
       
        // Cria um novo elemento para o histórico
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.textContent = prediction;
       
        // Adiciona a cor baseada no valor
        const predValue = parseFloat(prediction);
        if (predValue >= 1.00 && predValue <= 1.59) {
            historyItem.classList.add('blue-number');
        } else if (predValue >= 2.00 && predValue <= 9.59) {
            historyItem.classList.add('purple-number');
        } else {
            historyItem.classList.add('pink-number');
        }
       
        // Adiciona ao início do histórico
        historyContainer.insertBefore(historyItem, historyContainer.firstChild);
    }
   
    // Função para atualizar a exibição do histórico
    function updateHistoryDisplay(historyList) {
        // Limpa o histórico atual
        historyContainer.innerHTML = '';
       
        // Adiciona cada item ao histórico
        historyList.forEach(prediction => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            historyItem.textContent = prediction;
           
            // Adiciona a cor baseada no valor
            const predValue = parseFloat(prediction);
            if (predValue >= 1.00 && predValue <= 1.59) {
                historyItem.classList.add('blue-number');
            } else if (predValue >= 2.00 && predValue <= 9.59) {
                historyItem.classList.add('purple-number');
            } else {
                historyItem.classList.add('pink-number');
            }
           
            historyContainer.appendChild(historyItem);
        });
    }
   
    // Validação de formulários
    const phoneInputs = document.querySelectorAll('input[name="phone"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '').slice(0, 9);
        });
    });
});