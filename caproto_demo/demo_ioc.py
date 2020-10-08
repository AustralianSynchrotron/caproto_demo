""" Demo caproto EPICS ioc
Author: baldwinb
"""
import logging
from caproto.server import pvproperty, PVGroup
from caproto import ChannelType
from caproto.server import ioc_arg_parser, run
#from caproto.threading.client import Context

import numpy as np

logger = logging.getLogger(__name__)

# the prefix of the PVs hosted by this demo
#  change this if you get conflicts with others running the demo
PV_prefix = "CAPROTO_DEMO:"

class DemoIOC(PVGroup):
    """demo ioc """

    ACCEL = 0.1 # ie the motor will increment by this every 0.1s toward the set point

    analog_out_1 = pvproperty(value=0.1, record="ao", name="analog_out_1",precision=3)
    analog_in_1 = pvproperty(value=0.1, record="ai", name="analog_in_1",precision=3, read_only=True)
    motor = pvproperty(value=0.0, record="motor", name="motor")
    waveform_an_1 = pvproperty(value=[0.0], record="waveform", name="waveform", max_length=1024, read_only=True)
    status_str = pvproperty(value=" ", record="waveform", name="status_str", max_length=100)
    
    def __init__(self, prefix, **kwargs):
        super().__init__(prefix, **kwargs)
        
        # this is the simulated external reading, that is 
        #  loopback between an_1_out and an_1_in set and readback, say between +/-10V
        self.actual_voltage_1 = 0.1 # [V] 
        
        # simulated real motor position 
        self.actual_motor_pos = 0.0 # [mm] 

        # an1 reads into this
        self.an1_array = np.zeros(1024)

        # index into the waveform for an1_in reading
        self.an1_index = 0 

    @motor.startup
    async def motor(self, instance, async_lib):
        """on startup load in the settings from yaml"""
        await self.motor.fields["EGU"].write("mm")
        await self.motor.fields["TWV"].write(1)
        await self.motor.fields["PREC"].write(3)
        await self.motor.fields["TWV"].write_metadata(precision=3)
        await self.motor.fields["RBV"].write_metadata(precision=3)
        #await self.motor.fields["VAL"].write_metadata(precision=3)

    # update the readback PV string whenever any of the input PVs change,
    @analog_in_1.scan(period=0.1)
    async def analog_in_1(self, instance, async_lib):
        """ update the analog_in_1 reading """

        an_1 = self.actual_voltage_1 + np.random.rand() * 0.01
        
        await self.analog_in_1.write(an_1)

        self.an1_array[self.an1_index] = an_1

        self.an1_index += 1
        if self.an1_index >=1024:
            self.an1_index = 0

        await self.waveform_an_1.write(self.an1_array)

        # also sim'ing the motor moving here, could be better somewhere else?
        # update the readback PV         
        current_pos = self.actual_motor_pos 
        target_pos = self.motor.value 
        
        # make it look like is is slowly moving to position
        if current_pos != target_pos:
            diff = target_pos - current_pos
            if diff > self.ACCEL:
                current_pos += self.ACCEL
                moving = True
            elif diff < -self.ACCEL:
                current_pos += -self.ACCEL
                moving = True
            else:
                current_pos = target_pos
                moving = False
        else:
            moving = False

        if self.motor.field_inst.done_moving_to_value.value != moving:
            await self.motor.field_inst.done_moving_to_value.write(moving)

        mtr_pos = current_pos + np.random.rand() * 0.01
        self.actual_motor_pos = current_pos
        await self.motor.fields["RBV"].write(mtr_pos)
        
        return self.actual_voltage_1

    @analog_out_1.putter
    async def analog_out_1(self, instance, value):
        logger.info(f"VAL: new an_1 pos= {value}")
        self.actual_voltage_1 = value
        return value

    @motor.putter
    async def motor(self, instance, value):
        """VAL position_set"""
        #self.actual_motor_pos = value

        logger.info(f"VAL: new motor pos= {value}")
        
        return value  # returning this indicates to the ui it was clipped

    
    @motor.fields.tweak_step_size.putter
    async def motor(fields, instance, value):
        """tweak_step_size motor.TWV"""
        logger.info(f"TWV: {value}")

    @motor.fields.tweak_motor_forward.putter
    async def motor(fields, instance, value):
        """ tweak_motor_forward motor.TWF """
        slf = fields.parent.group
        pos = slf.motor.value
        move_by = slf.motor.field_inst.tweak_step_size.value
        logger.info(f"TWF: TWV={move_by}, passing {pos+move_by} to VAL")
        await slf.motor.write(pos + move_by)

    @motor.fields.tweak_motor_reverse.putter
    async def motor(fields, instance, value):
        """ tweak_motor_reverse motor.TWR"""
        slf = fields.parent.group
        pos = slf.motor.value
        move_by = slf.motor.field_inst.tweak_step_size.value
        logger.info(f"TWR: TWV={move_by}, passing {pos-move_by} to VAL")
        await slf.motor.write(slf.motor.value - move_by)

    

if __name__ == "__main__":
    ioc_options, run_options = ioc_arg_parser(
        default_prefix=PV_prefix, desc="demo IOC using caproto"
    )
    print("ioc_options" + str(ioc_options))

    ioc = DemoIOC(**ioc_options)

    run_options["log_pv_names"] = True
    print("run_options:" + str(run_options))
    run(ioc.pvdb, **run_options)  # blocking

    print("end")
