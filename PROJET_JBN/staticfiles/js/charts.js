// Chart.js pour le graphique en anneau des paiements
document.addEventListener('DOMContentLoaded', function() {
    const paymentCtx = document.getElementById('paymentPieChart').getContext('2d');
    new Chart(paymentCtx, {
        type: 'doughnut',
        data: {
            labels: ['Demande de paiement', 'Paiement dû', 'Paiement reçu', 'Paiement en attente', 'Remboursé'],
            datasets: [{
                data: [20, 10, 30, 15, 25], // Données d'exemple
                backgroundColor: [
                    '#3E63DD', // primary-blue
                    '#F44336', // danger-color
                    '#4CAF50', // success-color
                    '#FFC107', // warning-color
                    '#2196F3'  // info-color
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%', // Transforme en graphique en anneau
            plugins: {
                legend: {
                    display: false // Masquer la légende par défaut
                },
                tooltip: {
                    enabled: true
                }
            }
        }
    });

    // Chart.js pour le graphique linéaire de présence des étudiants
    const studentsAttendanceCtx = document.getElementById('studentsAttendanceChart').getContext('2d');
    new Chart(studentsAttendanceCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil'],
            datasets: [{
                label: 'Présence des Étudiants',
                data: [65, 59, 80, 81, 56, 55, 40], // Données d'exemple
                fill: true,
                backgroundColor: 'rgba(62, 99, 221, 0.2)', // Fond bleu clair
                borderColor: '#3E63DD', // Ligne bleu principal
                tension: 0.4, // Ligne lissée
                pointRadius: 0, // Pas de points
                pointHoverRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        display: false
                    }
                }
            }
        }
    });

    // Chart.js pour le graphique linéaire de présence des professeurs
    const teachersAttendanceCtx = document.getElementById('teachersAttendanceChart').getContext('2d');
    new Chart(teachersAttendanceCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil'],
            datasets: [{
                label: 'Présence des Professeurs',
                data: [40, 50, 70, 60, 80, 75, 90], // Données d'exemple
                fill: true,
                backgroundColor: 'rgba(238, 130, 238, 0.2)', // Fond violet clair
                borderColor: '#EE82EE', // Ligne violette
                tension: 0.4, // Ligne lissée
                pointRadius: 0, // Pas de points
                pointHoverRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        display: false
                    }
                }
            }
        }
    });
});