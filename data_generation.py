from models.board import Board
from models.topic import Topic
from models.user import User


def main():
    u = User.find_one()
    for i in range(10):
        b= Board.new(dict(
            title='board_{}'.format(i)
        ))
        for j in range(100):
            Topic.new(dict(
                title='topic_{}'.format(i),
                board_id=b.id,
                content='topic_{}'.format(i),
                user_id=u.id
            ))


if __name__ == '__main__':
    main()