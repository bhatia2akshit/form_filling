import { Component } from '@angular/core';
import { TabContainerComponent } from './tab-container/tab-container.component';


@Component({
  selector: 'app-root',
  imports: [ TabContainerComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'frontend';
  analysisResults: any[] = [];

  

  onFilesSubmitted(results: any) {
    this.analysisResults = results;
  }
}
