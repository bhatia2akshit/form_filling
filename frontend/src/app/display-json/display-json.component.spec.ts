import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DisplayJsonComponent } from './display-json.component';

describe('DisplayJsonComponent', () => {
  let component: DisplayJsonComponent;
  let fixture: ComponentFixture<DisplayJsonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DisplayJsonComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DisplayJsonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
