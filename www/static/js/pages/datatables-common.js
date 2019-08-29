// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable(
    {
      lengthMenu: [ 100, 300, 2000 ],
      displayLength: 100
    }
  );
});
