import { Component } from '@angular/core';
import { ConfigService } from '../services/config.service';
import { MatListModule } from '@angular/material/list';

@Component({
  selector: 'app-display-json',
  imports: [MatListModule],
  templateUrl: './display-json.component.html',
  styleUrl: './display-json.component.scss'
})
export class DisplayJsonComponent {
  // List out all the jsons present in the saved directory.
  files = [1,2,3]

  // downloadFile(file: {name: string, file: File}): void {
  //   const url = URL.createObjectURL(file.file);
  //   const a = document.createElement('a');
  //   a.href = url;
  //   a.download = file.name;
  //   a.click();
  //   URL.revokeObjectURL(url);
  // }

}
