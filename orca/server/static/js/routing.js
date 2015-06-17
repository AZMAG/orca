var Grapnel = require('grapnel');
var React = require('react');

var SchemaApp = require('./schema.js');
var TableApp = require('./table.js');
var ColumnApp = require('./column.js');

var router = new Grapnel();

function content_div() {
  return document.getElementById('content');
}

router.get('', function(req) {
  React.render(<SchemaApp />, content_div());
});

router.get('tables/:table', function(req) {
  var table_name = req.params.table;
  React.render(<TableApp table={table_name} />, content_div());
});

router.get('tables/:table/columns/:column', function(req) {
  var table_name = req.params.table;
  var col_name = req.params.column;
  React.render(
    <ColumnApp table={table_name} column={col_name} />, content_div());
});
