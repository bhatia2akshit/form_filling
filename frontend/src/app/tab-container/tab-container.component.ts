import { Component } from '@angular/core';
import { PdfUploaderComponent } from '../pdf-uploader/pdf-uploader.component';
import { DisplayJsonComponent } from "../display-json/display-json.component";
import { MatListModule } from '@angular/material/list';
import { MatTabsModule } from '@angular/material/tabs';


@Component({
  selector: 'app-tab-container',
  imports: [PdfUploaderComponent, DisplayJsonComponent, MatListModule, MatTabsModule],
  templateUrl: './tab-container.component.html',
  styleUrls: ['./tab-container.component.scss']
})
export class TabContainerComponent {
  activeTabIndex = 0;

  onTabChanged(event: any) {
    this.activeTabIndex = event.index;
  }

  handleFiles(files: File[]) {
    console.log('Files to process:', files);
  }
}