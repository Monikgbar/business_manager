document.addEventListener('DOMContentLoaded', () => {
    const editCategoryModal = document.getElementById('editCategoryModal');
    editCategoryModal.addEventListener('show.bs.modal', (event) => {
        const button = event.relatedTarget; // Button that opened the modal
        const categoryId = button.getAttribute('data-category-id');
        const categoryName = button.getAttribute('data-category-name');
        const categoryColor = button.getAttribute('data-category-color');

        // Update the values in the form
        const modalForm = editCategoryModal.querySelector('form');
        modalForm.action = `/service/edit_category/${categoryId}/`;
        // Assign values to the form fields
        modalForm.querySelector('#categoryName').value = categoryName || '';
        modalForm.querySelector('#categoryColor').value = categoryColor || '#000000';
    });
});