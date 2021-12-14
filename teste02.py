from sqlalchemy import Column, Integer, String, update, delete
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, ForeignKey
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from asyncio import run

url_do_banco = 'sqlite+aiosqlite:///db.db'

engine = create_async_engine(url_do_banco)

session = sessionmaker(
    engine,
    expire_on_commit=False,
    future = True,
    class_ = AsyncSession,
    )


Base = declarative_base()

class Pessoa(Base):
    __tablename__ = 'pessoa'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    idade = Column(Integer)
    email = Column(String(100))
    posts = relationship('Post', backref='pessoa')

    def __repr__(self):
        return f'Pessoa({self.nome})'

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    titulo = Column(String(100))
    conteudo = Column(String(100))
    autor_id = Column(Integer, ForeignKey('pessoa.id'))
    autor = relationship('Pessoa', backref='post')

    def __repr__(self):
        return f'Post({self.titulo})'

async def create_database():
    async with engine.begin() as conn:
        """O que vai rolar quando conectar"""
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def criar_pessoa(nome, email):
    async with session() as s:
        s.add(Pessoa(nome=nome, email=email))
        await s.commit()

async def buscar_pessoa(nome):
    async with session() as s:
        query = await s.execute(
            select(Pessoa).where(Pessoa.nome == nome)
        )
        return query.scalars().all()

async def atualizar_nome(nome_antigo, nome_novo):
    async with session() as s:
        await s.execute(
            update(Pessoa).where(
                Pessoa.nome == nome_antigo
            ).values(nome=nome_novo)
        )
        await s.commit()

async def deletar_pessoa(nome):
    async with session() as s:
        await s.execute(
            delete(Pessoa).where(
                Pessoa.nome == nome
            )
        )
        await s.commit()

async def buscar_post_por_autor(nome):
    async with session() as s:
        query = await s.execute(
            select(Post, Pessoa).join(
                Post.author
            ).where(
                Pessoa.nome == nome
            )
        )
        result = query.all()
        return result



#run(create_database())

#run(criar_pessoa('Leonardo', 'leonardoperes1@gmail.com'))
#run(criar_pessoa('Peres', 'peresteste@gmail.com'))

#print(run(buscar_pessoa('Leonardo')))

#print(run(atualizar_nome('Leonardo', 'Leonardo Peres')))

#print(run(atualizar_nome('Leonardo Peres')))

print(run(buscar_post_por_autor('Leonardo')))