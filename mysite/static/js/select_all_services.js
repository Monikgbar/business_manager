document.addEventListener('DOMContentLoaded', function() {
		const selectAllCheckboxes = document.querySelectorAll('.select-all');

		selectAllCheckboxes.forEach(selectAll => {
			selectAll.addEventListener('change', function(){
			    const categoryId = this.getAttribute('data-category');
			    const checkboxes = document.querySelectorAll(`.category-${categoryId}`);

			    checkboxes.forEach(checkbox => {
			        checkbox.checked = this.checked;
                });
            });
        });
    });