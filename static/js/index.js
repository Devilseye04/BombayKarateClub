// function removeDuplicateRows($table) {
//   function getVisibleRowText($row) {
//     return $row.find("td:visible").text().toLowerCase();
//   }

//   $table.find("tr").each(function (index, row) {
//     var $row = $(row);
//     $row.nextAll("tr").each(function (index, next) {
//       var $next = $(next);
//       if (getVisibleRowText($next) == getVisibleRowText($row)) $next.remove();
//     });
//   });
// }

// removeDuplicateRows($("#attendenceTable"));

// function showTableData() {
//   document.getElementById("info").innerHTML = "";
//   var myTab = document.getElementById("attendence");

//   // LOOP THROUGH EACH ROW OF THE TABLE AFTER HEADER.
//   for (i = 1; i < myTab.rows.length; i++) {
//     // GET THE CELLS COLLECTION OF THE CURRENT ROW.
//     var objCells = myTab.rows.item(i).cells;

//     // LOOP THROUGH EACH CELL OF THE CURENT ROW TO READ CELL VALUES.
//     for (var j = 0; j < objCells.length; j++) {
//       info.innerHTML = info.innerHTML + " " + objCells.item(j).innerHTML;
//     }
//     info.innerHTML = info.innerHTML + "<br />"; // ADD A BREAK (TAG).
//   }
// }

function removeDuplicates() {
  var t = document.getElementById("attendenceTable");
  var seen = [];
  var r = t.getElementsByTagName("tr");
  //   console.log(r.length);
  var arrLen = r.length;
  for (var i = 1; i < r.length; i++) {
    // console.log(i);
    var d = r[i].getElementsByTagName("td")[1].innerHTML;
    // console.log(d);
    if (seen.includes(d)) {
      r[i].remove();
      //   console.log("removed");
      i -= 1;
    } else {
      //   console.log("push");
      seen.push(d);
    }
    // console.log(seen);
  }
}

// jQuery(document).ready(function ($) {
//     // jQuery code is in here
//     var tableRows = $("#attendenceTable").find("tbody tr");
//     var seens = [];
//     for (var i = 0; i < tableRows.length; i++) {
//       var tRow = $(tableRows[i]);
//       var cell1Content = tRow.find("td").val();
//       console.log(cell1Content);
//       console.log(seens);
//       if (seens.indexOf(cell1Content) != -1) {
//         tRow.remove();
//       } else {
//         seens.push(cell1Content);
//       }
//     }
//   });
