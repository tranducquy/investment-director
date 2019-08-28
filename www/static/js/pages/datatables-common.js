// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable(
    {
      lengthMenu: [ 50, 200, 1000 ],
      displayLength: 50
    }
  );
});
