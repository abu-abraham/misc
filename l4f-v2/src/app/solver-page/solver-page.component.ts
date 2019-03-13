import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-solver-page',
  templateUrl: './solver-page.component.html',
  styleUrls: ['./solver-page.component.scss']
})
export class SolverPageComponent implements OnInit {

  public windowSize: number;

  constructor() { }

  ngOnInit() {
    this.windowSize = window.innerWidth;
  }

}
