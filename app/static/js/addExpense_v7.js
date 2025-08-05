document.addEventListener('DOMContentLoaded', () => {
    const addBtn = document.getElementById('add-button');
    const overlay = document.getElementById('overlay');
    const body = document.querySelector('body');
    const backBtn = document.getElementById('back-btn');
    const subBtn = document.getElementById('submit-btn');

    const selectedExpenseCategory = document.getElementById('expense-category')
    const container = selectedExpenseCategory.closest('.container')
    const customCategoryContainer = container.nextElementSibling
    const customCategory = customCategoryContainer.querySelector('#custom-category')
    
    const showDropdown = document.getElementById('show-dropdown')

    addBtn.addEventListener('click', () => {
        overlay.classList.remove('hidden'); 
        overlay.classList.add('flex');

        customCategoryContainer.classList.remove('flex');
        customCategoryContainer.classList.add('hidden');
        container.classList.remove('hidden');
        container.classList.add('flex');

        selectedExpenseCategory.selectedIndex = 0;
        customCategory.value = '';
        document.getElementById('amount').value = '0';
        document.getElementById('comment').value = '';
    });

    selectedExpenseCategory.addEventListener('change', function () {
        if (this.value == 'other') {
            container.classList.remove('flex');
            container.classList.add('hidden');

            customCategory.required = true
 
            customCategoryContainer.classList.remove('hidden');
            customCategoryContainer.classList.add('flex');
        } else{
            customCategoryContainer.classList.remove('flex');
            customCategoryContainer.classList.add('hidden');

            customCategory.value = ''
            customCategory.required = false

            container.classList.remove('hidden');
            container.classList.add('flex');
        }
    });

    showDropdown.addEventListener('click', () => {
        customCategoryContainer.classList.remove('flex');
        customCategoryContainer.classList.add('hidden');

        selectedExpenseCategory.selectedIndex = 0
                
        container.classList.remove('hidden');
        container.classList.add('flex');
    })

    backBtn.addEventListener('click', () => {
        overlay.classList.replace('flex', 'hidden');
    });

    subBtn.addEventListener('click', (e) => {
        
        const commentVal = document.getElementById('comment').value;
        if (selectedExpenseCategory.value == 'other' && customCategory.value.length > 50){
            e.preventDefault();
            alert('Maximum characters exceeded! Atmost 50 characters accpeted for Custom Category Name.')
        }
        else if (commentVal.length > 255) {
            e.preventDefault();
            alert('Maximum characters exceeded! Atmost 255 characters accepted for a Comment.')
        }
    })

    function openEditOverlay(id) {
        const editOverlay = document.getElementById(`edit-expense-overlay-${id}`);
        
        editOverlay.classList.remove('hidden');
        editOverlay.classList.add('flex');

        const editSelectedExpenseCategory = document.getElementById(`edit-exp-category-${id}`);
        const editContainer = editSelectedExpenseCategory.closest('.edit-container')
        const editCustomCategoryContainer = editContainer.nextElementSibling;
        const editCustomCategory = editCustomCategoryContainer.querySelector(`#edit-custom-category-${id}`)

        const showEditDropdown = document.getElementById(`show-edit-dropdown-${id}`)
        
        const currentValue = editSelectedExpenseCategory.value;
        if (currentValue === 'other') {
            // Show input, hide dropdown
            editContainer.classList.remove('flex');
            editContainer.classList.add('hidden');

            editCustomCategoryContainer.classList.remove('hidden');
            editCustomCategoryContainer.classList.add('flex');
            editCustomCategory.required = true;
        } else {
            // Show dropdown, hide input
            editContainer.classList.remove('hidden');
            editContainer.classList.add('flex');

            editCustomCategoryContainer.classList.add('hidden');
            editCustomCategoryContainer.classList.remove('flex');
            editCustomCategory.required = false;
        }
        

        editSelectedExpenseCategory.addEventListener('change', function () {
            if (this.value == 'other') {
                editContainer.classList.remove('flex');
                editContainer.classList.add('hidden');

                editCustomCategory.value = '';
                editCustomCategory.required = true;
                
                editCustomCategoryContainer.classList.remove('hidden');
                editCustomCategoryContainer.classList.add('flex');
            } else{
                editCustomCategoryContainer.classList.remove('flex');
                editCustomCategoryContainer.classList.add('hidden');

                editCustomCategory.value = ''
                editCustomCategory.required = false
                
                editContainer.classList.remove('hidden');
                editContainer.classList.add('flex');
            }
        });

        showEditDropdown.addEventListener('click', () => {
            editCustomCategoryContainer.classList.remove('flex');
            editCustomCategoryContainer.classList.add('hidden');

            editSelectedExpenseCategory.selectedIndex = 0
                
            editContainer.classList.remove('hidden');
            editContainer.classList.add('flex');
        })

        const editBackBtn = document.getElementById(`edit-back-btn-${id}`)

        editBackBtn.addEventListener('click', () => {
            editOverlay.classList.replace('flex', 'hidden')
        })

        const editSubBtn = document.getElementById(`edit-submit-btn-${id}`);
        editSubBtn.addEventListener('click', (e) => {
        
        const editCommentVal = document.getElementById(`edit-comment-${id}`).value;
        if (editSelectedExpenseCategory.value == 'other' && editCustomCategory.value.length > 50){
            e.preventDefault();
            alert('Maximum characters exceeded! Atmost 50 characters accpeted for Custom Category Name.')
        }
        else if (editCommentVal.length > 255) {
            e.preventDefault();
            alert('Maximum characters exceeded! Atmost 255 characters accepted for a Comment.')
        }
    })
    }
    window.openEditOverlay = openEditOverlay;

    // category button options
    const categoryButtons = document.querySelectorAll('.category-btn')
    const expenseItems = document.querySelectorAll('.expense-item')
    let currentCategory = null

    categoryButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const selectedBtn = btn.dataset.category;

            if (selectedBtn == currentCategory) {
                currentCategory = null
                updateUI(currentCategory);
                return

            } else{
                currentCategory = selectedBtn
                updateUI(currentCategory) 
            }
        }) 
    });

    function updateUI(category){
        categoryButtons.forEach(btn => {
            btn.classList.remove(
                'bg-[hsl(0,0%,15%)]',
                'text-[hsl(0,0%,70%)]',
                'scale-90')
            btn.classList.add(
                'bg-[hsl(0,0%,10%)]',
                'text-[hsl(0,0%,95%)]',
                'hover:bg-gradient-to-t',
                'from-[hsl(0,0%,10%)]',
                'to-[hsl(0,0%,15%)]')
        })

        if(category){
            const activeBtn = document.querySelector(`.category-btn[data-category="${category}"]`)
            if (activeBtn) {
                activeBtn.classList.remove(
                'bg-[hsl(0,0%,10%)]',
                'text-[hsl(0,0%,95%)]',
                'hover:bg-gradient-to-t',
                'from-[hsl(0,0%,10%)]',
                'to-[hsl(0,0%,15%)]'
                )
                activeBtn.classList.add(
                'bg-[hsl(0,0%,15%)]',
                'text-[hsl(0,0%,70%)]',
                'scale-90'
                )
            }
        }

        expenseItems.forEach(item => {
            const itemCategory = item.dataset.category;

            if(!category || itemCategory.trim().toLowerCase() === category.trim().toLowerCase()){
                item.classList.remove('hidden')
            }else {
                item.classList.add('hidden')
            }
        })
    }
});