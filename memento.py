from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from random import sample
from string import ascii_letters


class Originador:
    """
    O Originador mantém um estado importante que pode mudar ao longo do tempo. 
    Ele também define um método para salvar o estado dentro de um memento e 
    outro para restaurar o estado a partir dele.
    """

    _estado = None
    """ 
    Para simplificar, o estado do originador é armazenado dentro de uma única 
    variável.
    """

    def __init__(self, estado: str) -> None:
        self._estado = estado
        print(f"Originador: Meu estado inicial é: {self._estado}")

    def fazer_algo(self) -> None:
        """
        A lógica de negócio do Originador pode afetar seu estado interno. 
        Portanto, o cliente deve fazer backup do estado antes de executar 
        métodos da lógica de negócios via o método salvar().
        """

        print("Originador: Estou fazendo algo importante.")
        self._estado = self._gerar_string_aleatoria(30)
        print(f"Originador: e meu estado mudou para: {self._estado}")

    @staticmethod
    def _gerar_string_aleatoria(tamanho: int = 10) -> str:
        return "".join(sample(ascii_letters, tamanho))

    def salvar(self) -> Memento:
        """
        Salva o estado atual dentro de um memento.
        """
        return MementoConcreto(self._estado)

    def restaurar(self, memento: Memento) -> None:
        """
        Restaura o estado do Originador a partir de um objeto memento.
        """
        self._estado = memento.obter_estado()
        print(f"Originador: Meu estado mudou para: {self._estado}")


class Memento(ABC):
    """
    A interface Memento fornece uma maneira de recuperar os metadados do 
    memento, como a data de criação ou o nome. No entanto, ela não expõe o 
    estado do Originador.
    """

    @abstractmethod
    def obter_nome(self) -> str:
        pass

    @abstractmethod
    def obter_data(self) -> str:
        pass


class MementoConcreto(Memento):
    def __init__(self, estado: str) -> None:
        self._estado = estado
        self._data = str(datetime.now())[:19]

    def obter_estado(self) -> str:
        """
        O Originador usa este método ao restaurar seu estado.
        """
        return self._estado

    def obter_nome(self) -> str:
        """
        Os demais métodos são usados pelo Histórico para exibir metadados.
        """
        return f"{self._data} / ({self._estado[0:9]}...)"

    def obter_data(self) -> str:
        return self._data


class Historico:
    """
    O Histórico não depende da classe MementoConcreto. Portanto, ele não tem 
    acesso ao estado do Originador armazenado dentro do memento. Ele trabalha 
    com todos os mementos através da interface base Memento.
    """

    def __init__(self, originador: Originador) -> None:
        self._mementos = []
        self._originador = originador

    def fazer_backup(self) -> None:
        print("\nHistórico: Salvando o estado do Originador...")
        self._mementos.append(self._originador.salvar())

    def desfazer(self) -> None:
        if not len(self._mementos):
            return

        memento = self._mementos.pop()
        print(f"Histórico: Restaurando estado para: {memento.obter_nome()}")
        try:
            self._originador.restaurar(memento)
        except Exception:
            self.desfazer()

    def mostrar_historico(self) -> None:
        print("Histórico: Aqui está a lista de mementos:")
        for memento in self._mementos:
            print(memento.obter_nome())


if __name__ == "__main__":
    originador = Originador("Texto-inicial-do-editor.")
    historico = Historico(originador)

    historico.fazer_backup()
    originador.fazer_algo()

    historico.fazer_backup()
    originador.fazer_algo()

    historico.fazer_backup()
    originador.fazer_algo()

    print()
    historico.mostrar_historico()

    print("\nCliente: Agora, vamos reverter!\n")
    historico.desfazer()

    print("\nCliente: Mais uma vez!\n")
    historico.desfazer()
