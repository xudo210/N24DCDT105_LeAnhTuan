"""DT087 - Xoa nut BST, chon successor la khoa nho nhat cay con phai.
Quy uoc: khoa nguyen phan biet, cay rong cao 0, nut la cao 1.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Nut:
    khoa: int
    trai: Optional['Nut'] = None
    phai: Optional['Nut'] = None


@dataclass
class ThongKe:
    so_sanh_tim: int = 0
    so_buoc_ke_vi: int = 0
    truong_hop: str = 'khong_tim_thay'
    ke_vi: Optional[int] = None


def chen(g: Optional[Nut], x: int) -> Nut:
    """Chen khoa x vao BST. Khoa trung se bi tu choi."""
    if type(x) is not int:
        raise ValueError('Khoa phai la so nguyen.')
    if g is None:
        return Nut(x)
    if x < g.khoa:
        g.trai = chen(g.trai, x)
    elif x > g.khoa:
        g.phai = chen(g.phai, x)
    else:
        raise ValueError(f'Khoa trung: {x}')
    return g


def tao_cay(day: list[int]) -> Optional[Nut]:
    if len(day) > 100:
        raise ValueError('Chi nhan toi da 100 khoa.')
    if any(type(x) is not int for x in day) or len(day) != len(set(day)):
        raise ValueError('Day phai gom cac khoa nguyen phan biet.')
    g = None
    for x in day:
        g = chen(g, x)
    return g


def nho_nhat(g: Nut, tk: Optional[ThongKe] = None) -> Nut:
    """Tra ve nut trai nhat cua cay con khong rong, khong sua lien ket."""
    if g is None:
        raise ValueError('Khong tim min cua cay rong.')
    nut = g
    while nut.trai is not None:
        if tk is not None:
            tk.so_buoc_ke_vi += 1
        nut = nut.trai
    return nut


def xoa(g: Optional[Nut], x: int, tk: Optional[ThongKe] = None) -> Optional[Nut]:
    """Tra goc moi. Khi co hai con, copy khoa successor va xoa nut successor cu.
    Tk chi thong ke thao tac chinh, khong tinh duyet kiem chung.
    """
    if type(x) is not int:
        raise ValueError('Khoa xoa phai la so nguyen.')
    if tk is None:
        tk = ThongKe()

    def _xoa(nut: Optional[Nut], khoa: int, dang_xoa_ke_vi: bool = False) -> Optional[Nut]:
        if nut is None:
            return None
        if not dang_xoa_ke_vi:
            tk.so_sanh_tim += 1
        if khoa < nut.khoa:
            nut.trai = _xoa(nut.trai, khoa, dang_xoa_ke_vi)
        elif khoa > nut.khoa:
            nut.phai = _xoa(nut.phai, khoa, dang_xoa_ke_vi)
        else:
            if nut.trai is None and nut.phai is None:
                if not dang_xoa_ke_vi:
                    tk.truong_hop = 'la'
                return None
            if nut.trai is None or nut.phai is None:
                if not dang_xoa_ke_vi:
                    tk.truong_hop = 'mot_con'
                return nut.trai if nut.trai is not None else nut.phai
            if not dang_xoa_ke_vi:
                tk.truong_hop = 'hai_con'
            ke_vi = nho_nhat(nut.phai, tk)
            if not dang_xoa_ke_vi:
                tk.ke_vi = ke_vi.khoa
            nut.khoa = ke_vi.khoa
            nut.phai = _xoa(nut.phai, ke_vi.khoa, True)
        return nut

    return _xoa(g, x)


def duyet_giua(g: Optional[Nut]) -> list[int]:
    if g is None:
        return []
    return duyet_giua(g.trai) + [g.khoa] + duyet_giua(g.phai)


def dem_nut(g: Optional[Nut]) -> int:
    if g is None:
        return 0
    return 1 + dem_nut(g.trai) + dem_nut(g.phai)


def chieu_cao(g: Optional[Nut]) -> int:
    if g is None:
        return 0
    return 1 + max(chieu_cao(g.trai), chieu_cao(g.phai))


def kiem_bst(g: Optional[Nut], can_duoi=None, can_tren=None) -> bool:
    if g is None:
        return True
    if can_duoi is not None and g.khoa <= can_duoi:
        return False
    if can_tren is not None and g.khoa >= can_tren:
        return False
    return kiem_bst(g.trai, can_duoi, g.khoa) and kiem_bst(g.phai, g.khoa, can_tren)


def ve_cay_chu(g: Optional[Nut], muc: int = 0, nhan: str = 'ROOT') -> str:
    if g is None:
        return ('    ' * muc) + f'{nhan}: rong\n'
    kq = ('    ' * muc) + f'{nhan}: {g.khoa}\n'
    if g.trai is not None or g.phai is not None:
        kq += ve_cay_chu(g.trai, muc + 1, 'L')
        kq += ve_cay_chu(g.phai, muc + 1, 'R')
    return kq
