import { Component, OnInit, Input } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import * as $ from 'jquery';
import { ConfigService } from '../config.service';

@Component({
    selector: 'app-solver',
    templateUrl: './solver.component.html',
    styleUrls: ['./solver.component.scss'],
    host: {
        '(document.keypress)': 'handlee($event)'
    }
})
export class SolverComponent implements OnInit {

    myControl = new FormControl;
    public value;
    public save_solution;
    public submit_to_class;
    public check_syntax;
    public solve;

    @Input()
    windowSize: number;

    constructor(private config: ConfigService) {
    }

    ngOnInit() {
        console.log(this.windowSize);
        if (this.windowSize > 500) {
            this.save_solution = "Save Solution";
            this.submit_to_class = "Submit to Class";
            this.check_syntax = "Check Syntax";
            this.solve = "Solve";
        }


        this.myControl.valueChanges.subscribe(x => {
            console.log(x);
        });


        $("#constraint_editor").on("keydown keyup", function (e) {
            if (e.keyCode == 32) {
                var text = $(this).text().replace(/[\s]+/g, " ").trim();
                var word = text.split(" ");
                var newHTML = "";
                console.log(word);
                $.each(word, function (index, value) {
                    switch (value.toUpperCase()) {
                        case "AND":
                        case "OR":
                        case "NOT":
                            newHTML += "<span style='color:red'>" + value + "&nbsp;</span>";
                            break;
                        case "(":
                        case ")":
                            newHTML += "<span style='color:green'>" + value + "&nbsp;</span>";
                            break;
                        default:
                            newHTML += "<span class='other'>" + value + "&nbsp;</span>";
                    }
                });
                $(this).html(newHTML);

                //// Set cursor postion to end of text
                var child = $(this).children();
                var range = document.createRange();
                var sel = window.getSelection();
                range.setStart(child[child.length - 1], 1);
                range.collapse(true);
                sel.removeAllRanges();
                sel.addRange(range);
                $(this)[0].focus();
            }
        });


    }

    public onSolve(): void {
        console.log(document.querySelector("#sort_editor").textContent);
        console.log(document.querySelector("#vocab_editor").textContent);
        console.log(document.querySelector("#constraint_editor").textContent);
        console.log(this.config.getSettings());

    }

}
