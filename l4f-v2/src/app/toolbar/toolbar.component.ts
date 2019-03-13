import { Component, OnInit, HostListener } from '@angular/core';

@Component({
  selector: 'app-toolbar',
  templateUrl: './toolbar.component.html',
  styleUrls: ['./toolbar.component.scss']
})

export class ToolbarComponent implements OnInit {
  innerWidth;
  name;
  constructor() { 
    this.name= "Name";
  }

  @HostListener('window:resize', ['$event'])
  onResize(event) {
    this.innerWidth = window.innerWidth;
  }

  public onLogout() :void {
    sessionStorage.clear();
  }
  ngOnInit() {
    this.innerWidth = window.innerWidth;
    if (this.name == null)
      this.name = sessionStorage.getItem("name");
  }

}
