import { Document } from 'src/app/document/entities/document.entity';
import { Column, Entity, ManyToOne, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class Chunk {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column()
  content!: string;

  @Column()
  order!: number;

  @Column()
  tsv!: string;

  @Column({
    type: 'vector',
    nullable: true,
  })
  embedding!: number[];

  @ManyToOne(() => Document, { onDelete: 'CASCADE' })
  document!: Document;
}
