#coding: utf-8

""" 演示了这个基础库的基本操作。
目前基本库已经能够满足大部分的需求。但是还不支持事务。
如果出现了不能满足的，可以去修改进一步完善
"""
from rkplatform.base.database import Database

def action1(request):
    db = Database() # 初始化db
    try:
        """
         这里完成你的业务逻辑，分别使用
         db.save
         db.delete
         db.update
         db.find_all
         db.find_one
         db.execute
         注意: 上述的方法中，需要db_shard，table_shard, 
          可以通过使用 rkplatform.base.utils 里面的方法来或得。
          具体的操作，请参考测试代码: rkplatform.tests.unit.test.database 
         """
    except:
        """ 这里处理你的异常信息
        """
    finally:
        db.close() #记住一定要关闭db，否则会有内存泄露


def action2(request):
    """ 在action1中，需要自己去显示的调用db.close()，为了防止忘记调用。
        所以，可以采用with...as...的方式来进行待用。
    """
    with Database() as db:
        """
         这里完成你的业务逻辑，分别使用
         db.save
         db.delete
         db.update
         db.find_all
         db.find_one
         db.execute
         注意: 上述的方法中，需要db_shard，table_shard, 
          可以通过使用 rkplatform.base.utils 里面的方法来或得。
          具体的操作，请参考测试代码: rkplatform.tests.unit.test.database 
        """
        pass

if __name__ == '__main__':
    pass

