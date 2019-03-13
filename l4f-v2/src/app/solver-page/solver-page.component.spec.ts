import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SolverPageComponent } from './solver-page.component';

describe('SolverPageComponent', () => {
  let component: SolverPageComponent;
  let fixture: ComponentFixture<SolverPageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SolverPageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SolverPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
