document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('date').textContent = new Date().toLocaleDateString('en-GB');

    createHorizontalBarChart('skillsChart', 'Top Required Skills', skillData, 'rgba(54, 162, 235, 0.6)');
    createBarChart('salaryChart', 'Average Salary by Region', salaryData, 'rgba(75, 192, 192, 0.6)');
    createPieChart('seniorityChart', 'Position Levels', seniorityData);
    createHorizontalBarChart('responsibilityChart', 'Main Responsibilities', responsibilityData, 'rgba(153, 102, 255, 0.6)');
});

function createHorizontalBarChart(canvasId, title, data, backgroundColor) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: title,
                data: Object.values(data),
                backgroundColor: backgroundColor,
                borderColor: backgroundColor.replace('0.6', '1'),
                borderWidth: 1
            }]
        },
        options: {
            maintainAspectRatio: false,
            indexAxis: 'y',
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    title: { display: true, text: 'Mentions Count' }
                }
            }
        }
    });
}

function createBarChart(canvasId, title, data, backgroundColor) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: title,
                data: Object.values(data),
                backgroundColor: backgroundColor,
                borderColor: backgroundColor.replace('0.6', '1'),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Salary (RUB)' }
                }
            }
        }
    });
}

function createPieChart(canvasId, title, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(data),
            datasets: [{
                data: Object.values(data),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: { display: true, text: title }
            }
        }
    });
}
