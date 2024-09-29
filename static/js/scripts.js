document.addEventListener('DOMContentLoaded', function() {
    // Prepare the category data and post counts from Django
    const categoryPostCounts = [
        {% for item in category_post_counts|slice:":6" %}
        {
            category: "{{ item.category|escapejs }}",
            post_count: {{ item.post_count }}
        }{% if not forloop.last %},{% endif %}
        {% endfor %}
    ];

    // Extract categories and post counts into separate arrays
    const categories = categoryPostCounts.map(item => item.category);
    const postCounts = categoryPostCounts.map(item => item.post_count);

    // Get the canvas element by its ID
    const ctx = document.getElementById('categoryBarChart').getContext('2d');

    // Create a new bar chart using Chart.js
    const categoryBarChart = new Chart(ctx, {
        type: 'bar', // Chart type
        data: {
            labels: categories, // Categories as labels
            datasets: [{
                label: 'Number of Posts', // Legend label
                data: postCounts, // Data points (post counts)
                backgroundColor: 'rgba(75, 192, 192, 0.2)', // Bar fill color
                borderColor: 'rgba(75, 192, 192, 1)', // Bar border color
                borderWidth: 1 // Border width
            }]
        },
        options: {
            responsive: true, // Make the chart responsive
            scales: {
                y: {
                    beginAtZero: true // Y-axis starts at 0
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.raw + ' posts'; // Tooltip displays post count
                        }
                    }
                }
            }
        }
    });
});
