import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { DocumentService } from '../services/document.service';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';


@Component({
  selector: 'app-pdf-uploader',
  standalone: true,
  imports: [
    CommonModule,
    MatIconModule,
    MatButtonModule,
    MatListModule,
    MatProgressBarModule,
    MatSnackBarModule
  ],
  templateUrl: './pdf-uploader.component.html',
  styleUrls: ['./pdf-uploader.component.scss']
})
export class PdfUploaderComponent {
  uploadedFiles: {name: string, file: File}[] = [];
  isDragging = false;
  isLoading = false;
  @Output() filesSubmitted = new EventEmitter<File[]>();

  constructor(
    private documentService: DocumentService,
    private snackBar: MatSnackBar
  ) {}

  
  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files) {
      this.handleFiles(input.files);
    }
  }


  onDragOver(event: DragEvent): void {
    event.preventDefault();
    this.isDragging = true;
  }


  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    this.isDragging = false;
  }


  onDrop(event: DragEvent): void {
    event.preventDefault();
    this.isDragging = false;
    if (event.dataTransfer?.files) {
      this.handleFiles(event.dataTransfer.files);
    }
  }


  private handleFiles(files: FileList): void {
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      if (file) {
        this.uploadedFiles.push({name: file.name, file});
      }
    }
  }


  removeFile(index: number): void {
    this.uploadedFiles.splice(index, 1);
  }


  downloadFile(file: {name: string, file: File}): void {
    const url = URL.createObjectURL(file.file);
    const a = document.createElement('a');
    a.href = url;
    a.download = file.name;
    a.click();
    URL.revokeObjectURL(url);
  }


  submitFiles(): void {
    if (this.uploadedFiles.length === 0) return;
    const files = this.uploadedFiles.map(f => f.file);
    this.documentService.analyzeDocuments(files).subscribe({
      next: (response) => {
        this.snackBar.open('Documents analyzed successfully!', 'Close', {
          duration: 3000
        });
        this.filesSubmitted.emit(files); // Emit after successful upload
      },
      error: (error) => {   
        this.snackBar.open('Error analyzing documents', 'Close', {
          duration: 3000
        });
        console.error('Error:', error);
      }
    });
  }
}