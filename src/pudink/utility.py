def collides(first, second):
    return (
        first.x < second.x + second.width
        and first.x + first.width > second.x
        and first.y < second.y + second.height
        and first.y + first.height > second.y
    )
