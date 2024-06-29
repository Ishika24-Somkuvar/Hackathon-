document.getElementById('calorieForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Get user inputs
    let age = parseInt(document.getElementById('age').value);
    let height = parseInt(document.getElementById('height').value);
    let weight = parseInt(document.getElementById('weight').value);
    let gender = document.getElementById('gender').value;
    let activityLevel = document.getElementById('activity').value;

    // Calculate BMR (Basal Metabolic Rate) based on gender
    let bmr;
    if (gender === 'male') {
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age);
    } else if (gender === 'female') {
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age);
    }

    // Adjust BMR based on activity level
    let activityFactor;
    switch (activityLevel) {
        case 'sedentary':
            activityFactor = 1.2;
            break;
        case 'lightlyActive':
            activityFactor = 1.375;
            break;
        case 'moderatelyActive':
            activityFactor = 1.55;
            break;
        case 'veryActive':
            activityFactor = 1.725;
            break;
        case 'superActive':
            activityFactor = 1.9;
            break;
        default:
            activityFactor = 1.2; // Default to sedentary
            break;
    }

    // Calculate daily calories needed
    let calories = Math.round(bmr * activityFactor);

    // Display results
    document.getElementById('bmrResult').textContent = `Your Basal Metabolic Rate (BMR) is approximately ${Math.round(bmr)} calories per day.`;
    document.getElementById('caloriesResult').textContent = `To maintain your weight, you need about ${calories} calories per day.`;
    document.getElementById('recommend').innerHTML = '<h3>Now we have to go to <a href="#diet">Diet Recommendation system</a> to fulfill your calorie intake needs.</h3>';
    document.getElementById('result').classList.remove('hidden');
});
