document.addEventListener('DOMContentLoaded', function(){
    const addBtn = document.getElementById('add-button')
    const overlay = document.getElementById('overlay')
    const body = document.querySelector('body')
    const backBtn = document.getElementById('back-btn')

    const selectBudgetCategory = document.getElementById('budget-category');
    const container = selectBudgetCategory.closest('.container');
    const customCategoryContainer = container.nextElementSibling;
    const customCategory = customCategoryContainer.querySelector('#custom-category')

    const showDropdown = document.getElementById('show-dropdown')
    
    addBtn.addEventListener('click', () => {
        overlay.classList.remove('hidden')
        overlay.classList.add('flex')

        customCategoryContainer.classList.remove('flex');
        customCategoryContainer.classList.add('hidden');
        container.classList.remove('hidden');
        container.classList.add('flex');        

        selectBudgetCategory.selectedIndex = 0
        customCategory.value = ''
        document.getElementById('amount').value = '0';
        document.getElementById('comment').value = '';
    })

    selectBudgetCategory.addEventListener('change', function(){
        if (this.value == 'other') {
            container.classList.remove('flex');
            container.classList.add('hidden');
            
            customCategory.required = true;

            customCategoryContainer.classList.remove('hidden');
            customCategoryContainer.classList.add('flex');
        } else{
            container.classList.remove('hidden');
            container.classList.add('flex');
            
            customCategory.value = '';
            customCategory.required = false;

            customCategoryContainer.classList.remove('flex');
            customCategoryContainer.classList.add('hidden');
        }
    })

    showDropdown.addEventListener('click', () => {
        customCategoryContainer.classList.remove('flex');
        customCategoryContainer.classList.add('hidden');

        selectBudgetCategory.selectedIndex = 0
                
        container.classList.remove('hidden');
        container.classList.add('flex');
    })

    backBtn.addEventListener('click', () => {
        overlay.classList.replace('flex', 'hidden');
    })

    function openEditOverlay(id){
        const editOverlay = document.getElementById(`edit-budget-overlay-${id}`)

        editOverlay.classList.remove('hidden')
        editOverlay.classList.add('flex')
        
        const editSelectedBudgetCategory = document.getElementById(`edit-budget-category-${id}`)
        const editContainer = editSelectedBudgetCategory.closest('.edit-container')
        const editCustomCategoryContainer = editContainer.nextElementSibling;
        const editCustomCategory = editCustomCategoryContainer.querySelector(`#edit-custom-category-${id}`);

        const showEditDropdown = document.getElementById(`show-edit-dropdown-${id}`)

        const currentValue = editSelectedBudgetCategory.value;
        if (currentValue === 'other') {
            // Show input, hide dropdown
            editContainer.classList.add('hidden');
            editContainer.classList.remove('flex');

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
        
        editSelectedBudgetCategory.addEventListener('change', function(){
            if (this.value == 'other') {
                editContainer.classList.remove('flex')
                editContainer.classList.add('hidden')

                editCustomCategory.value = '';
                editCustomCategory.required = true;

                editCustomCategoryContainer.classList.remove('hidden')
                editCustomCategoryContainer.classList.add('flex')
            } else{
                editCustomCategoryContainer.classList.remove('flex')
                editCustomCategoryContainer.classList.add('hidden')
                
                editCustomCategory.value = '';
                editCustomCategory.required = false;
                
                editContainer.classList.remove('hidden')
                editContainer.classList.add('flex')
            }
        })

        showEditDropdown.addEventListener('click', () => {
            editCustomCategoryContainer.classList.remove('flex');
            editCustomCategoryContainer.classList.add('hidden');

            editSelectedBudgetCategory.selectedIndex = 0
                
            editContainer.classList.remove('hidden');
            editContainer.classList.add('flex');
        })

        const editBackBtn = document.getElementById(`edit-back-btn-${id}`)

        editBackBtn.addEventListener('click', () => {
            editOverlay.classList.replace('flex', 'hidden')
        })
    }
    window.openEditOverlay = openEditOverlay;

    // category button options
    const categoryButtons = document.querySelectorAll('.category-btn')
    const budgetItems = document.querySelectorAll('.budget-item')
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
                'to-[hsl(0,0%,15%)]')
                activeBtn.classList.add(
                'bg-[hsl(0,0%,15%)]',
                'text-[hsl(0,0%,70%)]',
                'scale-90')
            }
        }

        budgetItems.forEach(item => {
            const itemCategory = item.dataset.category;

            if(!category || itemCategory.trim().toLowerCase() === category.trim().toLowerCase()){
                item.classList.remove('hidden')
            }else {
                item.classList.add('hidden')
            }
        })
    }
})