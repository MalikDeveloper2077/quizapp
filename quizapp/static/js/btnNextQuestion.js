// Script for checking if a user selected an answer

let btnNext = document.querySelector('.answers__btn');

btnNext.addEventListener('click', function (e) {
    let prob_selected_answer = document.querySelector('.answer_selected');

    if (!prob_selected_answer) {
        e.preventDefault();

        let prob_paragraph = document.querySelector('.no_selected_answer');

        if (!prob_paragraph) {
            // If the document doesn't have paragraph with a class no_selected_answer
            // Create paragraph that says please select a answer
            paragraph = document.createElement('p');
            paragraph.innerHTML = 'Пожалуйста выберите 1 из вариантов';
            paragraph.classList.add('no_selected_answer');

            // Append under the question
            question = document.querySelector('.question');
            question.append(paragraph);
        }
    }
})