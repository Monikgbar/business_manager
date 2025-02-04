document.addEventListener('DOMContentLoaded', function() {
    const createSupplierButton = document.querySelector('#createSupplier');
    const editSupplierButton = document.querySelectorAll('#editSupplier');
    const deleteSupplierButton = document.querySelectorAll('#deleteSupplier');

    if (createSupplierButton) {
        createSupplierButton.addEventListener('click', function() {
            supplierForm.reset();
            supplierIdInput.value = '';
            submitButton.textContent = 'Guardar Proveedor';
        });
    }

    editSupplierButton.forEach(button => {
        button.addEventListener('click', function() {
            const supplierId = this.getAttribute('data-id');
            const supplierName = this.getAttribute('data-name');

            // Set the supplier name in the modal input
            supplierNameInput.value = supplierName;

            // Update the form action URL dynamically to the correct supplier
            editSupplierForm.action = `/stock/edit_supplier/${supplierId}/`;
        });
    });

    deleteSupplierButton.forEach(button => {
        button.addEventListener('click', function() {
            const supplierId = this.getAttribute('data-id');
            const supplierName = this.getAttribute('data-name');

            const confirmDelete = confirm(`¿Estás seguro de que desear eliminar al proveedor "${supplierName}"?`);
            if (confirmDelete) {
                window.location.href = `/stock/delete_supplier/${supplierId}/`;
            }
        });
    });
});