// Script for select a answer

let answers = document.querySelectorAll('.answer');

answers.forEach(item => {
    item.addEventListener('click', function () {
        let selected_answer = document.querySelector('.answer_selected');

        if (selected_answer) {
            // if the document already has a selected answer 
            selected_answer.classList.remove('answer_selected');
        }

        this.classList.add('answer_selected');
    })
})