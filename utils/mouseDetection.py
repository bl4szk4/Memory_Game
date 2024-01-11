
def mouse_detection(element_position: tuple, element_size: tuple, mouse_position: tuple) -> bool:
    """Function to return if mouse is focused on element like board's square or a button

    :param element_position list of elements coordinates
    :param element_size float of the element's size
    :param mouse_position tuple of mouse's position

    :return boolean"""

    e_x = element_position[0]
    e_y = element_position[1]
    m_x = mouse_position[0]
    m_y = mouse_position[1]

    if element_size[1]:
        if e_x <= m_x <= e_x + element_size[0] and e_y <= m_y <= e_y + element_size[1]:
            return True
        else:
            return False
    else:
        if e_x <= m_x <= e_x + element_size[0] and e_y <= m_y <= e_y + element_size[0]:
            return True
        else:
            return False
