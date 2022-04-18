import io
import sys

''' Convert tsv file of parrenger list provided by @Cartogenealogy
into a html file using jquery datatables.

Input from stdin,
output to stdout.

This code is released under the MIT License: https://opensource.org/licenses/MIT
Copyright (c) 2022 John A. Andrea
v1.0
'''

def output_header():
    print( '''
<!DOCTYPE html>
<html>
<head>
<title>Passenger lists</title>
<script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/v/dt/dt-1.11.5/datatables.min.css"/>
<script type="text/javascript" src="https://cdn.datatables.net/v/dt/dt-1.11.5/datatables.min.js"></script>
</head>
<body>
1749-52 Passenger Lists to Halifax collected into a single list by
<a href="https://www.facebook.com/Cartogenealogy/">@Cartogenealogy</a> / Keenan
as described here on the
<a href="https://www.facebook.com/groups/2301758491">Nova Scotia Genealogy</a> Facebook page.
<br><br>
<table id="docs" class="display" style="width:100%">
''' )

def output_trailer():
    print( '''
</table>
<script>
$(document).ready(function() {
    $('#docs').DataTable( {
        initComplete: function () {
            this.api().columns().every( function () {
                var column = this;
                var select = $('<select><option value=""></option></select>')
                    .appendTo( $(column.footer()).empty() )
                    .on( 'change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );
 
                        column
                            .search( val ? '^'+val+'$' : '', true, false )
                            .draw();
                    } );
 
                column.data().unique().sort().each( function ( d, j ) {
                    select.append( '<option value="'+d+'">'+d+'</option>' )
                } );
            } );
        }
    } );
} );
</script>
</body>
</html>
''' )

def to_html_entity( text ):
    # 'encode' function return byte array, use 'decode' to get back to an ascii string
    return text.encode( 'ascii', 'xmlcharrefreplace' ).decode( 'ascii' )


def encode_text( s ):
    s = s.strip()
    if s:
       return to_html_entity( s.replace('&', '&amp;').replace('<','&lt;').replace('>','&gt;') ).strip()
    else:
       return( '&nbsp;' )


output_header()

n_lines = 0
n_items = 0

indent = ' '

# collect the header items for the top and bottom of the table
header_row = ''

#for line in sys.stdin:
for line in io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8'):
    line = line.strip()
    if line:
       n_lines += 1
       if n_lines == 1:
          for item in line.split( '\t' ):
              n_items += 1
              # skip the first column
              if n_items > 1:
                 # extra space to be the same as the print statement
                 header_row += indent + ' <th>' + encode_text(item) + '</th>\n'
          print( '<thead><tr>' )
          print( header_row )
          print( '</tr></thead>' )
          print( '<tbody>' )
       else:
          print( '<tr>' )
          first = True
          m = 0
          for item in line.split( '\t' ):
              m += 1
              if m > 1:
                 print( indent, '<td>' + encode_text(item) + '</td>' )
          if m < n_items:
             # pad out to the number of columns in the header
             for i in range( n_items-m ):
                 print( indent, '<td>&nbsp;</td>' )
          print( '</tr>' )

print( '</tbody>' )
print( '<tfoot><tr>' )
print( header_row )
print( '</tr></tfoot>' )


print( 'per line', n_items, file=sys.stderr )
print( 'lines', n_lines, file=sys.stderr )

output_trailer()
