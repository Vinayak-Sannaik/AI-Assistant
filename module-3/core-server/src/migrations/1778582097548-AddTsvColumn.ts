import { MigrationInterface, QueryRunner } from 'typeorm';

export class AddTsvColumn1778582097548 implements MigrationInterface {
  name = 'AddTsvColumn1778582097548';

  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`
      ALTER TABLE chunk ADD COLUMN tsv tsvector;
    `);

    await queryRunner.query(`
      UPDATE chunk SET tsv = to_tsvector('english', content);
    `);

    await queryRunner.query(`
      CREATE INDEX idx_tsv ON chunk USING GIN(tsv);
    `);
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`DROP INDEX idx_tsv`);
    await queryRunner.query(`ALTER TABLE chunk DROP COLUMN tsv`);
  }
}
