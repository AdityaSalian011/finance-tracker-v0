document.addEventListener('DOMContentLoaded', function(){
    const monthlyIncome = document.getElementById('monthly-inc');
    const businessIncome = document.getElementById('business-inc');
    const freelanceIncome = document.getElementById('freelance-inc');
    const otherIncome = document.getElementById('other-inc');

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
            question.classList.replace('flex', 'hidden');
            response.classList.replace('hidden', 'flex');
    
            input.classList.replace('hidden', 'flex');
        })
        
        noBtn.addEventListener('click', () => {
            question.classList.replace('flex', 'hidden');
            response.classList.replace('hidden', 'flex');
            
            const income = response.querySelector('.income');
            income.value = '0';
            
            message.classList.replace('hidden', 'flex');
        })

        back.addEventListener('click', () => {
            const income = input.querySelector('.income');
            if (income) {
                income.value = '0';
            }
            input?.classList.replace('flex', 'hidden');
            message?.classList.replace('flex', 'hidden');
            response.classList.replace('flex', 'hidden');
            question.classList.replace('hidden', 'flex');
        })
    })
})