import { Component } from '@angular/core';
import { PdfUploaderComponent } from './pdf-uploader/pdf-uploader.component';
import { DisplayJsonComponent } from "./display-json/display-json.component";


@Component({
  selector: 'app-root',
  imports: [PdfUploaderComponent, DisplayJsonComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'frontend';
  analysisResults: any[] = [];

  handleFiles(files: File[]) {
    console.log('Files to process:', files);
  }

  onFilesSubmitted(results: any) {
    this.analysisResults = results;
  }
}
