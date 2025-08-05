document.addEventListener('DOMContentLoaded', function(){
    function hideElement(el){
        el.classList.add('hidden');
        el.classList.remove('flex', 'md:flex')
    }

    function showElement(el){
        el.classList.remove('hidden');
        el.classList.add('flex', 'md:flex')
    }

    document.querySelectorAll('[data-section]').forEach(sectionEl => {
        const name = sectionEl.dataset.section;
        
        const question = document.querySelector(`.question[data-section="${name}"]`);
        const response = document.querySelector(`.response[data-section="${name}"]`);
    
        const yesBtn = question.querySelector('.yes');
        const noBtn = question.querySelector('.no');
    
        const input = response.querySelector('.input');
        const message = response.querySelector('.message');
        const back = response.querySelector('.back');
    
        yesBtn.addEventListener('click', () => {
            hideElement(question);
            showElement(response);
    
            showElement(input);
        })
        
        noBtn.addEventListener('click', () => {
            hideElement(question);
            showElement(response);
            
            const income = response.querySelector('.income');
            income.value = '0';
            
            showElement(message);
        })

        back.addEventListener('click', () => {
            const income = response.querySelector('.income');
            if (income) {
                income.value = '0';
            }
            hideElement(input);
            hideElement(message);

            hideElement(response);
            
            showElement(question)
        })
    })
})