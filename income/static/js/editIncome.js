document.addEventListener('DOMContentLoaded', function(){
    const editOverlay = document.getElementById('edit-overlay')
    const editBackBtn = document.getElementById('edit-back-btn')
    
    function openEditOverlay(){
        editOverlay.classList.remove('hidden')
        editOverlay.classList.add('flex')
    }
    window.openEditOverlay = openEditOverlay

    editBackBtn.addEventListener('click', () => {
        editOverlay.classList.replace('flex', 'hidden')
    })
})