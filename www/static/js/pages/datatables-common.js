// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable(
    {
      lengthMenu: [ 50, 100, 200 ],
      displayLength: 50
    }
  );
});
